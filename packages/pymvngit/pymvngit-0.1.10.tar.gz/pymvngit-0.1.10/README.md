### Python Maven Git Tool
---
Tool to manage a group of Git/Maven projects together.

##### SYNTAX:
          pymvngit [MACRO | FUNCTION] {argument(s)}
##### EXAMPLES:
    pymvngit start
    pymvngit build-all
    pymvngit listProjects
    pymvngit listMacros summary
    pymvngit add-push -A Patch v0.5.7 "Bug Fix password field blank"
    pymvngit status-all
    pymvngit install-commons
    pymvngit ltags

**MACRO**: 
A sequence of Git/Maven commands to run sequentially over project(s) of a repository.  

**REPOSITORY**:
A collection of Git/Maven projects that can be managed together.

##### RUNNING
###### Functions
- **start**: Create a repository from the current directory. The current folder itself, and every first-level sub-folder, will be analyzed and if it's a Git/Maven project, will be part of this created repository. The name of the folder will be used to reference the project in Macros.
- **listProjects**: List the projects part of the repository associated with the current directory.

- **listMacros**: List the macros configured. 
  - arguments:
     - *"summary"*: list a summary of all commands on a single table
###### Macros     
- **[macro]**: Name of a macro to be executed.
As example, some default macros are already available. In order to manage the macros: adding, modifying or removing, use the command:
```bash
pymvngit editMacros      #or only emac for short
```
Structure of a Macro:
```json
"[INTERNAL-KEY]": {
    "key": "[NAME-MACRO]",
    "description": "[DESCRIPTION]",
    "executions": [
        {
            "tool": "[git OR maven]",
            "command": "[COMMAND]",
            "projects": ["NAME-PROJECT","NAME-PROJECT"]
        },
}
```
Examples of macros:
```json
"1": {
    "key": "tag-everyone",
    "description": "Tag all the projects",
    "executions": [
        {
            "tool": "git",
            "command": "tag -a $1 -m $2",
            ## When no project are informed, all of the repository are used
            "projects": []               
        }
    ]
},
"2": {
    "key": "commit-tag-customer",
    "description": "Commit everything and tag the CustomerVision and CustomerVisionFeign project",
    "executions": [
        {
            "tool": "git",
            "command": "add -A",
            "projects": ["customer-view","customer-view-feign"]               
        },
        {
            "tool": "git",
            "command": "commit -m $1",
            "projects": ["customer-view","customer-view-feign"]               
        },
        {
            "tool": "git",
            "command": "tag -a $2 -m $3",
            "projects": ["customer-view","customer-view-feign"]               
        }
    ]
},
"2": {
    "key": "all-once",
    "description": "Git status, commit, push for commons and clients",
    "executions": [
        {
            "tool": "git",
            "command": "status",
            "projects": ["commons","client"]
        },
        {
            "tool": "git",
            "command": "add $1",
            "projects": ["commons","client"]
        },
        {
            "tool": "git",
            "command": "commit -m $2",
            "projects": ["commons","client"]
        },
        {
            "tool": "git",
            "command": "push",
            "projects": ["commons","client"]
        },
        {
            "tool": "git",
            "command": "tag -a $3 -m $4",
            "projects": ["commons","client"]
        }
    ]
},
"3": {
    "key": "test_tag",
    "description": "Test Tag",
    "executions": [
        {
            "tool": "git",
            "command": "tag -a $1 -m $2",
            "projects": ["teachstore-commons"]
        }
    ]
}
```



