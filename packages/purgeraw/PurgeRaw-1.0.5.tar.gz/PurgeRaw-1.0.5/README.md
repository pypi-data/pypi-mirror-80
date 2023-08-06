**Overview**

For photographers keeping every raw file captured can use a lot of space.  
This utility allows a photographer to purge any unused raw files leaving 
only the processed files with their associated raws.

The app trawls the input directory for raw and processed images.
Where it finds a raw image with a numeric index that can't be
found in the processed images it is marked for removal.

Any sequence of 3 to 6 (inc) numbers in the image filename is deemed as its index which is used
to associate processed and raw images.

Processed images may also have a filename format with a range of indexes, e.g. IMG_01234-1236.jpg
This processed file would be associated with IMG_01234.cr3, IMG_01235.cr3 and IMG_01236.cr3 raw images
thus ensuring they are not deleted. This is useful for HDR or panoramic processed images.

For example, given the folder1 below:

<pre>
folder1/
  IMG_1000.cr3
  IMG_1001.cr3
  IMG_1002.cr3
  IMG_1003.cr3
  IMG_1004.cr3
  Processed/
    IMG_1000.jpg
    IMG_1002-1003.jpg
</pre>

Running `praw folder1 -d` would remove the IMG_1001.cr3 and 
IMG_1004.cr3 raw images as they don't have associated processed images.

The resulting directory would be left as:
<pre>
folder1/
  IMG_1000.cr3
  IMG_1002.cr3
  IMG_1003.cr3
  Processed/
    IMG_1000.jpg
    IMG_1002-1003.jpg
</pre>

To install run `pip install purgeraw`
