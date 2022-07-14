import fitz

def extract_notes(file_name):
    doc = fitz.open(file_name)

    # list to store the co-ordinates of all highlights
    highlights = []
    highlight_text = []

    # loop till we have highlight annotation in the page
    for page in doc:
        page_annots = list(page.annots())

        # sort page annots based on their location in the page
        # by default it is sorted based on create time
        page_annots.sort(key=lambda a: a.vertices[0][1])

        for annot in page_annots: 
            if annot.type[0] == 8:
                all_coordinates = annot.vertices

                if len(all_coordinates) == 4:
                    highlight_coord = fitz.Quad(all_coordinates).rect
                    highlights.append(highlight_coord)
                else:
                    all_coordinates = [all_coordinates[x:x+4] for x in range(0, len(all_coordinates), 4)]
                    for i in range(0,len(all_coordinates)):
                        coord = fitz.Quad(all_coordinates[i]).rect
                        highlights.append(coord)

        all_words = page.get_text_words()
        for h in highlights:
            sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersects(h)]
            highlight_text.append({ 'note': " ".join(sentence), 'link': "page: " + str(page.number + 1)})

        highlights = []
    # return "\n\n".join(highlight_text)
    return highlight_text
