# Wave Software Development Challenge

## Prerequisites
```
- Python3 (preferably the Conda distribution)
- Pip
```

## Technology Stack
```
- Jquery
- SemanticUI
- Flask
- Pandas
- SQLite
```

## Create environment and install dependencies
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Start server
```
$ FLASK_APP=server.py flask run
```

## Database Schema
### report table ###
| name | type |
| ---- | ---- |
| report_id | INTEGER |
| employee_id | INTEGER |
| period | TEXT |
| amount | REAL |

## Design decisions

I decided to implement my solution primarily in Python, making use of the Pandas data analysis library. Pandas provides a suite of tools that lends itself nicely to this problem space. Intially, I hoped to use the Luigi task framework, however this framework does not lend itself well to a small web applications - it is not designed to be triggered by RPC via a web application. 

On the frontend I kept my technology stack simple, opting to use Jquery instead of a full fledge framework. I used SemanticUI for styling as I believe this to be very clean and modern.

For the database I choose SQLite for ease-of-use - no installation required.

I am particularily proud of my "mini Task framework", found in `tasks.py`. Initially, I intended to use Luigi as I have some experience with this framework, however, I soon realized this would be overkill for the spirit of this challenge. I decided to implement my own mini framework with the only part of Luigi I needed - composable tasks.

If I had more time to explore this idea further, I would investigate if it's feasible for my mini framework to have a map method, such that:

```
map :: Task<A> -> Task<B>
```

Unlike my current solution, such an approach would ensure a consistent return type, and allow greater composability. However, I would need to research the most "pythonic" way to achieve my goal, as this approach is heavily influenced by functional programming languages, and may not actually be the best fit for a Python framework.
