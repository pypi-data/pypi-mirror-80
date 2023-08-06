from derobertis_cv.models.university import UniversityModel
from derobertis_cv.pldata.constants.institutions import UF_NAME, VCU_NAME
from derobertis_cv.pltemplates.logo import image_base64

UF = UniversityModel(UF_NAME, 'UF', 'Gainesville, FL', logo_base64=image_base64('uf-logo.png'))
VCU = UniversityModel(VCU_NAME, 'VCU', 'Richmond, VA', logo_base64=image_base64('vcu-logo.png'))