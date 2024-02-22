# Cyton Solver

## Table of Contents
- [Introduction](#introduction)
- [Repo Structure](#repo-structure)
- [Run App](#run-app)
- [Further Information](#further-information)
- [Contributing](#contributing)

## Introduction

When challenged with an infection, or cancer, our immune system needs to rapidly produce new immune cells to fight the attack. Once the pathogen is cleared, these cells need to die away. Immune cells have therefore evolved highly tuned strategies to determine when they should divide, how long they need to divide for and when they need to die. [Our lab](https://www.wehi.edu.au/laboratory/hodgkin-lab/) has developed a sophisticated mathematical model, called Cyton, that can extract the parameters underlying these fate decisions from experimental data.

The Cyton model is internationally recognised as a critical component in analysis and design of experiments of quantitative immune responses. The primary aim of this web application is to make the Cyton model more accessible to the scientific community. Researchers can utilize this user-friendly platform via their web browsers, facilitating seamless access to Cyton's capabilities from anywhere in the world.

## Repo Structure
```
cyton-solver/
├── README.md                         # <-- YOU ARE HERE
├── backend/                         
│   ├── api/                          # API Endpoints           
│   │   ├── endpoints/                # Main API Endpoints
│   │   └── support/                  # Functions for Endpoints
│   └── core/                         # Core Logic, Models
│            
└── frontend/                        
    ├── public/                       # Static Images/Icons
    └── src/
        ├── assets/
        ├── components/
        └── themes/
```

## Run App

### Backend
The project is built with Python version 3.9.12.

#### Create a Virtual Environment
```
python -m venv env
```

#### Activate the Virtual Environment
```
source ./env/bin/activate
```

#### Install Dependencies
```
pip install -r requirements.txt
```

#### Local Run 
```
python main.py
```       

### Frontend

#### Install Dependencies
```
npm install
```

#### Build App
#### Build App
```
npm run build
```

#### Local Run
#### Local Run
```
npm run dev
```

## Further Information

For a deeper understanding of the Cyton model and its applications, you may refer to the following paper:

- [Cyton2: A Model of Immune Cell Population Dynamics That Includes Familial Instructional Inheritance](https://www.frontiersin.org/articles/10.3389/fbinf.2021.723337/full)

## Contributing

### Branching Workflow
- ```main``` - this branch contains production code. All development code is merged into here after every sprint.
- ```dev``` - this branch contains pre-production code. All branches during every sprint are branched from here.

### Commit Message Format
To improve the readability of our commits, we use the following format:
```
<type>: <short summary>
  │             │
  │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       
  │       
  └─⫸ Commit Type: chore|docs|feat|fix|refactor|style
```

#### Type
* **chore**: Changes that do not affect the external user (e.g. updating the .gitignore file)
* **docs**: Changes to documentations (e.g. README.md)
* **feat**: A new feature
* **fix**: A bug fix
* **refactor**: A code change that neither fixes a bug nor adds a feature (e.g. renaming a variable)
* **style**: Changes that do not affect the meaning of the code such as code formatting (e.g. adding a white-space)