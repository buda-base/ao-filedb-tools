CREATE SCHEMA if not exists `content`;
use `content`;

CREATE TABLE `content`.`image_file_infos` (
  # image information
   `id`    INTEGER UNSIGNED auto_increment PRIMARY KEY,
  `storage_file_id` INTEGER UNSIGNED COMMENT 'storage.files.id FK',
  `image_type` ENUM ('jpg', 'png', 'single_image_tiff', 'jp2', 'raw') NOT NULL,
  `image_mode` ENUM ('1', 'L', 'RGB', 'RGBA', 'CMYK', 'P', 'OTHER') NOT NULL,
  `tiff_compression` ENUM ('raw', 'tiff_ccitt', 'group3', 'group4', 'tiff_lzw', 'tiff_jpeg', 'jpeg', 'tiff_adobe_deflate', 'lzma', 'other') COMMENT 'names are from PIL version 10',
  `width` smallint UNSIGNED NOT NULL COMMENT 'width of the bitmap (not taking a potential exif rotation into account)',
  `height` smallint UNSIGNED NOT NULL COMMENT 'height of the bitmap (not taking a potential exif rotation into account)',
  `quality` tinyint UNSIGNED COMMENT 'relevant only for jpg, png and single_image_tiff encoded as jpg: quality of encoding. JPEG is represented between 0 and 100. For PNG this column encodes the compression between 0 and 9.',
  `bps_x` tinyint UNSIGNED NOT NULL COMMENT 'bits per sample x',
  `bps_y` tinyint UNSIGNED NOT NULL COMMENT 'bits per sample y',
  `recorded_date` timestamp COMMENT 'the timestamp recorded in the exif metadata',
  create_time timestamp default CURRENT_TIMESTAMP null,
  update_time timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP

)COMMENT = 'Table containing information about image files';
ALTER TABLE `content`.`image_file_infos` ADD FOREIGN KEY (`storage_file_id`) REFERENCES `storage`.`files` (`id`);

CREATE TABLE `content`.`pdf_file_infos` (
  # image information
  `id` INTEGER UNSIGNED  auto_increment PRIMARY KEY,
  `number_of_pages` smallint UNSIGNED COMMENT 'the number of pages',
  `median_nb_chr_per_page` smallint UNSIGNED COMMENT 'the average number of characters in a page',
  `median_nb_images_per_page` smallint UNSIGNED COMMENT 'the average number of images per page',
  `recorded_date` timestamp COMMENT 'the timestamp recorded in the exif metadata',
  `storage_file_id` INTEGER COMMENT 'storage.files.id FK',
  create_time timestamp default CURRENT_TIMESTAMP null,
  update_time timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP

);
ALTER TABLE `content`.`pdf_file_infos` ADD FOREIGN KEY (`storage_file_id`) REFERENCES `storage`.`files` (`id`);
