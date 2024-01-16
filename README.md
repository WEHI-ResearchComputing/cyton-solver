# Cyton Solver

## Table of Contents
- [Introduction](#introduction)
- [Repo Structure](#repo-structure)
- [Run App](#run-app)
- [Further Information](#further-information)
- [Contributing](#contributing)

## Introduction
<!-- TO DO -->

## Repo Structure
```
cyton-solver/
├── README.md                         # <-- YOU ARE HERE
├── backend/                         
│   ├── api/                          # API Endpoints               
│   └── core/                         # 
│         
└── frontend/                        
    ├── public/                       # Static Images/Icons
    └── src/
        ├── components/
        ├── pages/
        ├── services/
        ├── styles/
        └── utils/
```

## Run App

### Install Dependencies
```
npm install
```

### Build App
```
npm run build
```

### Local Run
```
npm run dev
```

## Further Information

<!-- TO DO -->

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