import fitz

def extract_notes(file_name):
    data = {}

    doc = fitz.open(file_name)
    title = doc.metadata['title']
    data['title'] = title

    # list to store the co-ordinates of all highlights
    highlights = []
    data['highlights'] = []

    # loop till we have highlight annotation in the page
    for page in doc:
        page_annots = [a for a in list(page.annots()) if a.type[0] == 8]

        # sort page annots based on their location in the page
        # by default it is sorted based on create time
        page_annots.sort(key=lambda a: a and a.vertices[0][1])

        for annot in page_annots: 
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
        i = 0
        sentence = []

        for h in highlights:
            sentence.extend([w[4] for w in all_words if fitz.Rect(w[0:4]).intersects(h)])

            if i < len(highlights) - 1:
                next_h = highlights[i + 1]
                i += 1

                # Group near blocks together when the difference in y axis is less than 15 units
                if next_h.y0 - h.y0 < 15:
                    continue

            data['highlights'].append({ 'note': " ".join(sentence), 'link': "page: " + str(page.number + 1)})
            sentence = []

        highlights = []

    return data
