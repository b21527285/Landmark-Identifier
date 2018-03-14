# Natural Language Processing Lab - Assignment 1

We've developed a program that learns from consecuvite word patterns and applies this knowledge to generate new mails and evaluates the probabilities and perplexities of the new mails. All this proccess can be split into three parts: Training, generating, evaluating

## Training
The program trains on unigrams, bigrams and trigrams. The dataset is kept as a dictionary.

## Generating
Using the dictionaries created at training the program can generate new mails. For generating we put all possible words on a scale and generate a random number. Depending on which word the number corresponds to we generate a mail.

This leads to very meaningless mails with unigrams but the generated mails start getting meaningful with bigrams and trigrams (more with trigrams) as the previous words affect what the next word will be in bigrams and trigrams, unlike unigrams. But unfortunately even with trigrams the mails we generate don't tell us much.

## Evaluating
 For this part we use the dictionaries we've created at the training part, like the generating part. But this time the mails are real and actually make sense and since they weren't generated using our training data we can encounter grams for the first time. This means, according to our training data the probability of a mail that contains at least one unseen ngram will be *zero*. To overcome this problem we use add-one smoothing. There are other benefits of using this algorithm but overcoming this zero problem is the main one.

  This smoothing algorithm works like this: We imagine we had a different training set. A training set that contains every data we have on our real training set and more. In our imaginary training set every different ngram we've encountered on our original training set occurs one more time as well as the ngram we haven't encountered before but the test set has. This means even the probability of a mail which solely consists of ngrams we are encountering for the first time will have a probability bigger than zero. It'll be close to zero but *not* zero and that's we want.
  
  Now, the other benefit of this add-one smoothing is it brings the probabilities together to each other. For example if we have encountered an ngram 20 times out of 21 times and another ngram 1 time out of 21 times their unsmoothed probabilities will be 20/21 and 1/21 respectively. If we smooth these numbers the probabilities will be 21/22 and 2/22 respectively. The first ngram was dominating the probability scale, with smoothing it still dominates the scale but we've given the second ngram more space, we nearly doubled it!

## Perplexity
Perplexity is the inverse probability of the set, normalized by the number of words. We use perplexity to evaluate our language models. We normalize it because the perplexity is calculated as multiple multiplications, the more words/ngrams there are in the mail the more multiplications we need to do. And since our probabilities are small numbers the more we multiply the smaller a number we get. By dividing the probability by the number of words we ease this problem.

*\*This code only works for txt files with clean regex*
*The compatibility for csv files with dirty regex is under development*

  *Serhat Sağlık - 21527285*
  *Hacettepe University*
