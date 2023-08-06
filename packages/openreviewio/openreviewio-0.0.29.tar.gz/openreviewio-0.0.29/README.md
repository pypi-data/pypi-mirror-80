# /!\ Still in alpha stage and on its way to be stable. Every feedback is welcome!


# Overview
[OpenReviewIO](https://openreviewio-standard-definition.readthedocs.io/fr/latest/README.html) is a standard that describes a format for sharing media (shots, animations...) review informations. 
It's main purpose is to guarantee review informations compatibility across media reviewing tools.
Please read the specifications for more informations.

[OpenReviewIO Python API](https://pypi.org/project/openreviewio/) is the main Python API for the ORIO standard, maintained by the designer of the standard.

# Version
The version of the API is related to the version of the standard.  
`API 1.x.y <=> Standard 1.x`

**In Alpha stage, the API is 0.x.y but related to 1.x Standard. Will become 1.x.y when first stable release.**

Last standard version: [1.0](https://openreviewio-standard-definition.readthedocs.io/fr/latest/Version_1-0.html)

# Usage
```python
import openreviewio as orio
```

## Create a media review
```python
review = orio.MediaReview("/path/to/media.ext")
```

### Create a note
```python
note = orio.Note(author="Alice")
```

#### Create content

Contents are defined by the standard [version](https://openreviewio-standard-definition.readthedocs.io/fr/latest/Version_1-0.html)

*There is a naming [convention](https://openreviewio-standard-definition.readthedocs.io/fr/latest/Standard_Definition.html#contenu) about the contents:  
    - `Comment` means something related to the whole media.  
    - `Annotation` means something related to a specific frame and duration of the media.*

##### Text comment
```python
text_comment = orio.Content.TextComment(body="My text comment")
```

##### Image comment
```python
image = orio.Content.Image(path_to_image="/path/to/image_comment.png")
```

##### Image annotation
```python
image_annotation = orio.Content.ImageAnnotation(
    frame=17,
    duration=20,
    path_to_image="/path/to/image_annotation.png"
)
```

#### Add content to note
```python
# Single content
note.add_content(text_comment)

# Several contents
note.add_content([image, image_annotation])
```

### Add note to review
```python
review.add_note(note)
```

## Write media review to disk
```python
# Write next to the media
review.write()

# Specifying a directory
review.write("/path/to/review_dir")
```

## Export/Import a note as zip
```python
# Export
exported_note_path = note.export("/path/to/folder", compress=True)

# Import
review.import_note(exported_note_path)
```

# Examples
## From content to review
```python
# Content
text = orio.Content.TextComment(body="Banana")

# Note
new_note = orio.Note("Michel", content=text)

# Review
review = orio.MediaReview("/path/to/media.ext", note=new_note)
```

## Reply to a note 
```python
# Main note
text = orio.Content.TextComment(body="Make the logo bigger.")
main_note = orio.Note("Michel", content=text)

# Reply to the main note
reply = orio.Content.TextComment(body="Done, I'm waiting for my visibility payment.")
note_reply = orio.Note("Michel", content=reply, parent=main_note)
```

## Add a reference image to an image annotation

Useful for keeping an image as reference of the drawing.

```python
image_annotation = orio.Content.ImageAnnotation(
    frame=17,
    duration=20,
    path_to_image="/path/to/image_annotation.png",
    reference_image="/path/to/reference_image.png"
)
# Or
image_annotation.reference_image = "/path/to/reference_image.png"
```

Copyright 2020, Félix David ©