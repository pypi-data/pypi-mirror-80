## Colour Sort 

Generating Images using all 256<sup>3</sup> RGB colours, inspired by https://allrgb.com/

### Technique

To generate a re-coloured image, the source image's pixel data is sorted (using one of several different sorting modes) using numpy's `argsort` function, giving us a mapping from the original to the sorted version. This mapping is then used to "unsort" an array of all 256<sup>3</sup> colours that in sorted order. The result of this operation is then written out as our result.

### Installing

```
$ pip install colour_sort
```

### Running

Once the tool has been installed, it can be ran with the following command
```
$ colour generate --help
usage: colour generate [-h] [--sort {brightness,avg,rgb,rbg,brg,bgr,grb,gbr}]
                       infile outfile

positional arguments:
  infile
  outfile

optional arguments:
  -h, --help            show this help message and exit
  --sort {brightness,avg,rgb,rbg,brg,bgr,grb,gbr}

$ colour verify --help
usage: colour verify [-h] infile

positional arguments:
  infile

optional arguments:
  -h, --help  show this help message and exit
```
