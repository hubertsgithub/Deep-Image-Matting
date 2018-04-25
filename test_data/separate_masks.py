#from scipy import io
from skimage import io
import numpy as np

io.use_plugin('freeimage')

#input_file = "aachen_000000_000019_gtFine_instanceIds.png"
#input_file = "aachen_000000_000019_gtFine_instanceIds_cropped-C0PZM.png"
#input_file = 'test.png'

input_file = "aachen_000000_000019_gtFine_labelIds.png"
#input_file = "aachen_000000_000019_gtFine_labelIds_cropped-70P6S.png"
input_file = "aachen_000000_000019_gtFine_labelIds_cropped-NTHZ3.png"

#instance_id = 26010
img = io.imread(input_file, "I")
img = img.astype(np.uint16)
label_ids = set(img.flatten())
print label_ids

label_id = 26
if label_id:
    label_ids = [label_id]

orig = img.copy()
#orig = img.clone()
for label_id in label_ids:

    #img = 255*(img == 26010).astype(np.uint8)
    img = 255*(orig == label_id).astype(np.uint8)

    #io.imsave(input_file.replace('.png', '_{}.png'.format(instance_id)), img)
    output_name = input_file.replace('.png', '_{}.png'.format(label_id))
    print 'Saving to {}'.format(output_name)
    io.imsave(output_name, img)
