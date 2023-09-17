## CodeReviewer testing

This is a repo, where I looked at the predictions of the Microsofts CodeReviewer model. 
The original paper can be found [here](https://arxiv.org/abs/2203.09095).

I also tried to fine-tune it to understand Kotlin.

The whole process of what I did is described in the `testing.jpynb` notebook. 

I did everything locally in a conda environment apart from fine-tuning. For fine-tuning I used A100 GPU in Colab. 

The dependencies are: `pygithub`, `pytorch`, `transformers`, `evaluate`, `accelerate`. You can install them using `pip` or `conda`.