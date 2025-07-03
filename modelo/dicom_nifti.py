import os
import pydicom
import numpy as np
import nibabel as nib

def cargar_dicom_carpeta(ruta):
    slices = []
    for archivo in sorted(os.listdir(ruta)):
        if archivo.endswith(".dcm"):
            ds = pydicom.dcmread(os.path.join(ruta, archivo))
            slices.append(ds.pixel_array)
    volumen = np.stack(slices, axis=0)
    return volumen

def dicom_a_nifti(ruta_dicom, ruta_salida):
    volumen = cargar_dicom_carpeta(ruta_dicom)
    nifti_img = nib.Nifti1Image(volumen, affine=np.eye(4))
    nib.save(nifti_img, ruta_salida)
    return ruta_salida

def cargar_nifti(archivo_nifti):
    img = nib.load(archivo_nifti)
    data = img.get_fdata()
    return data