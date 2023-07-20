# rplace-template-maker
(works with [rplace-host-template](https://github.com/GiggioG/rplace-host-template))

1. Create a `coords` folder, in which for each template you create a `template.txt` file, which contains `x,y`.
2. Create a `raws` folder, in which you hold png files of your templates. Their names should be `template.png`.
3. Create a `templateList.json` file, being a JSON list of strings, which are the names of your templates.
4. Every time you add a new template to `raws` and `coords`, add it to the `templateList.json` and run `update.js`.
It finds new files and uploads file, and it only updates old files if they have been edited since the last time the script was run.