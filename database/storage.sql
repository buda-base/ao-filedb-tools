CREATE  SCHEMA if not exists `storage`;
use `storage`;

CREATE TABLE if not exists `storage`.`roots`
(
    `id`     INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT 'internal identifier of the root object',
    `name`   varchar(32) CHARACTER SET ascii NOT NULL COMMENT 'name of the Storage root (in ASCII), used to fint it on disk (ex: Archive0). The actual disk path depends on the mount points on the servers.',
    `layout` varchar(50) CHARACTER SET ascii NOT NULL COMMENT 'name of the storage layout, ASCII'
)  COMMENT 'Storage roots (ex: Archive 1)';

CREATE TABLE if not exists `storage`.`objects`
(
    # storage objects (ex: W123)
    `id`               INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT 'internal identifier',
    # TODO: Would be a good idea to make this an FK to a work object, even if it's only the works in this schema
    `bdrc_id`          varchar(32) NOT NULL COMMENT 'the BDRC RID (ex: W22084), unique persistent identifier, ASCII string no longer than 32 characters',
    `created_at`       timestamp COMMENT 'the timestamp of the creation of the object, or the equivalent object in a previous archive storage',
    `last_modified_at` timestamp COMMENT 'the timestamp of the last known modification',
    `root`             INTEGER UNSIGNED NOT NULL COMMENT 'the OCFL storage root id that the object is stored in'
) COMMENT 'Objects kept on archive storage';

CREATE UNIQUE INDEX `objects_index_0` ON `storage`.`objects` (`bdrc_id`, `root`);

ALTER TABLE `storage`.`objects`
    ADD FOREIGN KEY (`root`) REFERENCES `storage`.`roots` (`id`);


CREATE TABLE if not exists `storage`.`files`
(
    # files
    `id`               INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `digest`           binary(32)                NOT NULL COMMENT 'the digest of the file',
#    `digest_algorithm` ENUM ('sha256', 'sha512', 'sha1','md5','not_set')DEFAULT 'not_set' COMMENT 'the algorithm used to compute the digest',
    `size`             bigint UNSIGNED           NOT NULL COMMENT 'the size in bytes',
    `pronom_number`    smallint UNSIGNED        COMMENT 'the PRONOM number or, if unavailable, null',
    `persistent_id`    binary(32) UNIQUE         NOT NULL COMMENT 'The identifier is globally unique for the BDRC archive. By construction it is the sha256 or a random id in case of collision.',
    `created_at`       timestamp COMMENT 'the creation date of the file. Often unknown or unreliable, can be set to the earlier mtime exposed by the FS',
    `validity`         ENUM ('seemingly_valid', 'fully_valid', 'cannot_read', 'partially_recoverable','not_set') NOT NULL COMMENT 'the validity of the image',
    `earliest_mdate`   timestamp COMMENT 'the earliest modification date for the file (optional)'
) COMMENT = 'Table of all the (deduplicated) actual files handled by Archive Storage';
CREATE UNIQUE INDEX `files_index_1` ON `storage`.`files` (`digest`, `size`);


CREATE TABLE if not exists `storage`.`paths`
(
    # file paths in objects
    `id`            INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `file`           INTEGER UNSIGNED ,
    `storage_object` INTEGER UNSIGNED  ,
    `path`           varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT 'Unicode string (256 Unicode characters max) representing the (case sensitive) content paths in OCFL objects for each content file.',
    `image_group`    varchar(32) CHARACTER SET ascii COMMENT 'the BDRC image group RID (ex: I0886), unique persistent identifier, ASCII string no longer than 32 characters, when unknown set to NULL',
    `root_folder`    ENUM ('images', 'archive', 'sources', 'backup', 'eBooks', 'web', 'other') COMMENT 'should be obvious. other can be anything, not just the folder other'
) COMMENT 'File Paths of objects';
ALTER TABLE `storage`.`paths`
    ADD FOREIGN KEY (`file`) REFERENCES `storage`.`files` (`id`),
    ADD FOREIGN KEY (`storage_object`) REFERENCES `storage`.`objects` (`id`)
