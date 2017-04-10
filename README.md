# Chart GitHub Development Timelines

This repo consists of a simple utility that pings the GitHub API, fetches all issues for a given repository, then visualizes time estimates for those issues using Google Charts. These visualizations can then be used when planning with team members.

![Sample timeline](https://github.com/yaledhlab/development-timelines/raw/master/images/chart.png)

## Requirements

Python 2

## Usage

To use this repository, create one or more issues in a repository you control using the following format:

`{ESTIMATE OF HOURS TO CLOSE THE ISSUE} - Issue Title Here`

For example, `4 - Allow admins to edit buildings` would indicate that it should take 4 hours to allow admins to edit buildings.

Then obtain an access token for your account. Go to your user icon in the upper right of the navbar -> Settings -> Personal access tokens -> Generate new token. Click the 'repo' checkbox to grant your token read access to your repos.

Then paste your repo address and token into config.json; eg:

```
{
  "repo": "https://api.github.com/repos/YOUR_USERNAME/YOUR_REPOSITORY_NAME/issues",
  "access_token": "GET THIS STRING FROM GITHUB.COM -> SETTINGS -> PERSONAL ACCESS TOKENS",
  "use_saved_issue_json": "0"
}
```

Make sure there's no whitespace inside the value for access_token, then run:

```
python prepare_issue_json.py
```

This will generate (or overwrite) chart-data.json, a sample of which is present in this repo. Then just double click index.html to see your issues, ordered by their issue number and colored by their first assigned label (if any). 