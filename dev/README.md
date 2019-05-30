A big chunk of this work was based on:

https://github.com/MarkPrecursor/SRCNN-keras

I have made some changes and hope they work:

* Set different learning rates by layer as described in the original Paper, https://arxiv.org/abs/1501.00092
* The optimization I use is canonical to the paper, SGD.
* My subsampled data comes from a different source. It is not directly generated from the original image.
* I use images with one channel, so the work on removing the color treatment is on progress.
