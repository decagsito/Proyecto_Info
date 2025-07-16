import os
import pydicom
import numpy as np
import nibabel as nib

def cargar_dicom_carpeta(carpeta):
    archivos_dcm = []
    for f in os.listdir(carpeta):
        ruta = os.path.join(carpeta, f)
        if f.endswith(".dcm"):
            try:
                ds = pydicom.dcmread(ruta)
                orden = getattr(ds, 'InstanceNumber', None)
                if orden is None:
                    orden = getattr(ds, 'SliceLocation', None)
                archivos_dcm.append((orden, ds))
            except:
                continue

    # Ordenar por orden (InstanceNumber o SliceLocation)
    archivos_dcm.sort(key=lambda x: x[0] if x[0] is not None else 0)
    imagenes = [ds.pixel_array for _, ds in archivos_dcm]

    if not imagenes:
        raise ValueError("No se pudieron cargar imágenes DICOM válidas.")

    # Convertir a volumen 3D: (n_slices, height, width)
    volumen = np.stack(imagenes, axis=0).astype(np.float32)

    # Normalizar volumen a 0–255
    volumen = 255 * (volumen - np.min(volumen)) / (np.ptp(volumen) + 1e-5)
    return volumen.astype(np.uint8)

def dicom_a_nifti(ruta_dicom, ruta_salida):
    volumen = cargar_dicom_carpeta(ruta_dicom)
    nifti_img = nib.Nifti1Image(volumen, affine=np.eye(4))
    nib.save(nifti_img, ruta_salida)
    return ruta_salida

def cargar_nifti(archivo_nifti):
    img = nib.load(archivo_nifti)
    data = img.get_fdata()
    return data