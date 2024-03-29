from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os

def _add_thumb(s):
    """
    Modifies a string(filename,URL) containing an image filename, to insert '.thumb'
    """
    parts = s.split(".")
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)

class ThumbnailImageFieldFile(ImageFieldFile):
        
    def _get_thumb_path(self):
        return _add_thumb(self.path)
    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self):
        return _add_thumb(self.url)
    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)
        img.thumbnail(
            (self.field.thumb_width, self.field.thumb_height),
            Image.ANTIALIAS
        )
        img.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)
    

class ThumbnailImageField(ImageField):
    """
    Behaves like regular ImageField, but
    stores and extra (JPEG) thumbnail image,
    providing get_FIELD_thumb_url() and
    get_FIELD_thumb_filename().
    Accepts two additional, optional arguments:
    thumb_width and thumb_height,
    both defaulting to 128 (pixels). Resizing will
    preserve aspect ratio while staying inside the 
    requested dimensions; see PIL's Image.thumnail()
    method documentation for details.
    """ 
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)

    


