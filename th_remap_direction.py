# -*- coding: utf-8 -*-
"""
REMAP DIRECTION WHITEBOX TO TERRAHIDRO

@author: Mino
"""
import osgeo
import rasterio
import numpy as np

# Define the mapping dictionaries
remap_to_archydro = {
    1: 128,
    2: 1,
    4: 2,
    8: 4,
    16: 8,
    32: 16,
    64: 32,
    128: 64
}

remap_to_whitebox = {v: k for k, v in remap_to_archydro.items()}  # Reverse mapping

def remap_direction(fdr_wb, direction='to_archydro'):
    if direction == 'to_archydro':
        return remap_to_archydro.get(fdr_wb, fdr_wb)  # Forward mapping
    elif direction == 'to_whitebox':
        return remap_to_whitebox.get(fdr_wb, fdr_wb)  # Reverse mapping
    else:
        raise ValueError("Invalid direction. Use 'to_archydro' or 'to_whitebox'.")

#-------------------------------------------
# Define mapping dictionaries as arrays
max_value = 128  # Adjust this if you expect larger values
remap_array_archydro = np.full(max_value + 1, fill_value=-1)  # Default value for unmapped
for k, v in remap_to_archydro.items():
    remap_array_archydro[k] = v

remap_array_whitebox = np.full(max_value + 1, fill_value=-1)  # Default value for unmapped
for k, v in remap_to_whitebox.items():
    remap_array_whitebox[k] = v


def remap_direction_by_array(fdr_wb, direction='to_archydro'):
    if direction == 'to_archydro':
        return remap_array_archydro[fdr_wb]
    elif direction == 'to_whitebox':
        return remap_array_whitebox[fdr_wb]
    else:
        raise ValueError("Invalid direction. Use 'to_archydro' or 'to_whitebox'.")




# Read the input raster file
input_file = './03_th_final/th_fdr.tif'
output_file = './03_th_final/th_fdr_wb.tif'

# Select direction of mapping
#new_direction = 'to_archydro'
new_direction = 'to_whitebox'

with rasterio.open(input_file) as src:
    # Read the data into a NumPy array
    dir_data = src.read(1)  # Read the first band

    # Remap the values using the  vectorized + dict approach
    #vectorized_remap = np.vectorize(remap_direction)
    #remapped_data = vectorized_remap(dir_data, direction=new_direction)

    # Remap the values using array indexing for efficiency
    remapped_data = np.where(
        dir_data <= max_value,
        remap_array_archydro[dir_data],  # Use the appropriate remap array
        dir_data  # Keep original value if out of range
    )


    # Define metadata for the output file
    metadata = src.meta.copy()
    metadata.update({
        'dtype': 'uint8',  # Change to the appropriate dtype if needed
        'count': 1
    })

    # Write the remapped data to a new raster file
    with rasterio.open(output_file, 'w', **metadata) as dst:
        dst.write(remapped_data.astype(np.uint8), 1)  # Write to the first band

print("Remapping complete. Output saved to:", output_file)
