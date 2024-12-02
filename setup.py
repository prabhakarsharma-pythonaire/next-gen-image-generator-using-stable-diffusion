from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='This project uses the Stable Diffusion model to generate images based on text prompts. It employs a diffusion process and the CLIP text encoder to create visually coherent images from user input. By fine-tuning on custom datasets, the model can adapt its style for various applications, such as digital art, design, and content creation.',
    author='Ayush Kumar',
    license='MIT',
)
