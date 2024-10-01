#AO file tools

Define a schema for storing image statistics, and some tools for creating and accessing them.

## Requirements

[Requirements and Design](https://github.com/buda-base/ao-filedb-tools/issues/1)

### Images

Collect these features

| Attribute        | Description                                                                                                                                                                                         | data source | method           | data attribute                      |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|------------------|-------------------------------------|
| storage_file     | string of file path (root)                                                                                                                                                                          | import      | SQL update       | key of file                         | 
| format           | ('jpg', 'png', 'single_image_tiff', 'jp2', 'raw')                                                                                                                                                   | PIL         | PIL Image.open() | .format                             |
| mode             | ('1', 'L', 'RGB', 'RGBA', 'CMYK', 'P', 'OTHER')                                                                                                                                                     | PIL         | PIL Image.open() | .format                             |
| tiff_compression | ('raw', 'tiff_ccitt', 'group3', 'group4',<br/> 'tiff_lzw', 'tiff_jpeg', 'jpeg', 'tiff_adobe_deflate', 'lzma', 'other')                                                                              | PIL         | Image.open()     | .info.get('compression', 'unknown') |
| width            | width of the bitmap (not taking a potential exif rotation into account)'                                                                                                                            | PIL         | Image.open()     | .img.size[0]                        |
| height           | height of the bitmap (not taking a potential exif rotation into account)'                                                                                                                           | PIL         | Image.open()     | .img.size[1]                        |
| quality          | relevant only for jpg, png and single_image_tiff <br/>encoded as jpg: quality of encoding. JPEG is represented between 0 and 100.<br/>For PNG this column encodes the compression between 0 and 9.' | PIL         | Image.open       | .info.get('quality', 'unknown')     |
| bps              | 'bits per sample' aka resolution                                                                                                                                                                    | PIL         | Image.open()     | .info.get('dpi', 'unknown')         |
| recorded_date    | COMMENT 'the timestamp recorded in the exif metadata'                                                                                                                                               | PIL         | Image.open()     | img._getexif()                      |

### PDF
Collect these features

```mysql
  `number_of_pages` smallint UNSIGNED COMMENT 'the number of pages',
  `median_nb_chr_per_page` smallint UNSIGNED COMMENT 'the average number of characters in a page',
  `median_nb_images_per_page` smallint UNSIGNED COMMENT 'the average number of images per page',
  `recorded_date` timestamp COMMENT 'the timestamp recorded in the exif metadata'
```
| Attribute        | Description                                | data source | method         | data attribute  |
|------------------|--------------------------------------------|-------------|----------------|-----------------|
|number_of_pages | the number of pages                        |pypdf.PdfFileReader|                | .numPages       |
|median_nb_chr_per_page | the average number of characters in a page |pypdf.PdfFileReader|                | .numPages       |
|median_nb_images_per_page | the average number of images per page      |pypdf.PdfFileReader|                | .numPages       |
|recorded_date | the timestamp recorded in the meetadata    | pypdf.PdfFileReader| .document_info | ["/CreationDate"] |
