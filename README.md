# geo-extract-tester
A simple web-app to test geo extraction performance. The repo https://github.com/chicago-justice-project/article-tagging is the main consumer of this web app.

You can see the app running at https://geo-extract-tester.herokuapp.com/

## Initial setup

Set up a heroku app (see their instructions, they'll be better than anything I could write) using this repo. You only need to do this once.

## Updating

The app should be periodically updated with the new training/validation data as more data gets annotated.

Do this by downloading the most recent data dump and putting it into your local tagnews folder so it can be loaded. See https://github.com/chicago-justice-project/article-tagging for more detailed instructions on this part.

Once that's done, at the top level of this repo run

```
python train_test_split.py data/validation.txt data/training.txt /path/to/folder/containing/tagnews
```

Check your git diff and make sure it looks reasonable (you shouldn't see a full replacement in validation.txt/training.txt, but you should see the new articles being added).

If all looks good, commit to master, and push to **both** GitHub and Heroku.
