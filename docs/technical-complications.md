# Some technical complications

## Are these suggestions even correct?

We need a verification or at least an evaluation layer for the suggestions Shinx is creating. Verification is totally far fetched because an ideal verification flow would include copying the database into an isolated environment, running those queries and detecting any unwanted consequences and improvement in the query performance.

Therefore, for now we have decided to go with an evaluation layer. A separate agent with all the database structure and the query pattern will evaluate if the suggestions made by the primary agent are good or even viable. We can introduce a feedback loop here. Until the suggestions cross a threshold or exceed a preset looping cap, we can ask the primary agent to revise its suggestions based on the feedback produced by the evaluation agent. 
This will improve the quality of the suggestions.

## Supporting Multi-agent setup

In case we want to exploit all the opportunities I have mentioned within the Future section, a multi-agent setup will be a clean approach. 

## Distribution

Docker is a sane way to distribute Shinx. But I am uncertain if there is a better way to do so. Certainly not in a registry because we do not want it to get coupled to a particular language. In addition to this, we want to allow users to declare what they want. Since we are trying to support all SQL dialects, we want the user to declare what dialect they want. Depending on that, we will install the adapters. Something like: `sudo apt-get install shinx shinx[postgres].`

