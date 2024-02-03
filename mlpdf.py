import os, re, cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

path = r'C:\Users\paolo\Downloads'

def crop_and_merge_pdf(pdf, idx):
    pdf_label = convert_from_path(pdf, dpi=300)

    image_path = f'{path}\\pdf2img.jpg'
    cropped_image_path = f'{path}\\pdf2img_cropped.jpg'
    output_file = f'{path}\\ML_Label_{idx+1}.pdf'

    pdf_label[0].save(image_path, 'JPEG')
    pdf_image = cv2.imread(image_path)
    width, height = pdf_image.shape[:2]

    upper = pdf_image[0:height-270, 0:width]
    medium = pdf_image[height+70:height+460, 0:width]
    lower = pdf_image[height+830:2*height, 0:width]

    out = np.concatenate((upper, medium, lower), axis=0)
    cv2.imwrite(cropped_image_path, out)

    pdf_image = Image.open(cropped_image_path)
    rgb_pdf_image = pdf_image.convert('RGB')

    rgb_pdf_image.save(output_file)

    os.remove(image_path)
    os.remove(cropped_image_path)
    os.remove(pdf)

    return output_file.split('\\')[-1]

if __name__ == "__main__":
    pdfs = []
    pattern = re.compile(r'\w+_labels\.pdf$', re.IGNORECASE)
    for file in os.listdir(path):
        if pattern.search(file):
            pdfs.append(os.path.join(path, file))

    for idx, pdf in enumerate(pdfs):
        input_pdf = pdf.split('\\')[-1]
        print(f'Processing {input_pdf}...')
        print(f'{crop_and_merge_pdf(pdf, idx)} has been processed at Downloads.')