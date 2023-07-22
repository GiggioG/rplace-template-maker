require("dotenv").config();
const { execSync } = require("child_process");
const fs = require("fs");
const http = require("http");
// const host = "localhost:8080";
const host = "r-place-2022-bulgaria.herokuapp.com";

const stamp = Number(new Date()).toString();

let templates = require("./templateList.json");
if (!fs.existsSync("./lastUpdated")) { fs.mkdirSync("./lastUpdated"); }
templates.forEach(t => {
    if (!fs.existsSync(`./lastUpdated/${t}.coords.txt`)) {
        console.log(`${t} is new - uploading`);
        let [x, y] = String(fs.readFileSync(`./coords/${t}.txt`)).split(",").map(e => Number(e));
        let priority = Number(String(fs.readFileSync(`./priorities/${t}.txt`)));
        transformImage(t);

        let req_upload = http.request(`http://${host}/upload?imgname=${t}&x=${x}&y=${y}&priority=${priority}`, {
            method: "POST",
            headers: {
                "Content-Type": "image/png",
                "auth": process.env.PASSWORD
            }
        });
        let readStream = fs.createReadStream(`./_temp/${t}.template.png`);
        readStream.pipe(req_upload);
        req_upload.on("response", () => {
            let req_changeThumb = http.request(`http://${host}/changeThumb?imgname=${t}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "image/png",
                    "auth": process.env.PASSWORD
                }
            });
            let readStream2 = fs.createReadStream(`./_temp/${t}.colored.png`);
            readStream2.pipe(req_changeThumb);
        });

        fs.writeFileSync(`./lastUpdated/${t}.coords.txt`, stamp);
        fs.writeFileSync(`./lastUpdated/${t}.image.txt`, stamp);
        fs.writeFileSync(`./lastUpdated/${t}.priority.txt`, stamp);
    }
});

function updateCoords(t) {
    console.log(`Updating coords for ${t}`);
    let [x, y] = String(fs.readFileSync(`./coords/${t}.txt`)).split(",").map(e => Number(e));
    http.request(`http://${host}/move?imgname=${t}&x=${x}&y=${y}`, {
        method: "PATCH",
        headers: {
            "auth": process.env.PASSWORD
        }
    }).end();
    fs.writeFileSync(`./lastUpdated/${t}.coords.txt`, stamp);
}

function updatePriority(t){
    console.log(`Updating priority for ${t}`);
    let priority = Number(String(fs.readFileSync(`./priorities/${t}.txt`)));
    http.request(`http://${host}/priority?imgname=${t}&priority=${priority}`, {
        method: "PATCH",
        headers: {
            "auth": process.env.PASSWORD
        }
    }).end();
    fs.writeFileSync(`./lastUpdated/${t}.priority.txt`, stamp);
}

function transformImage(img) {
    if (!fs.existsSync("./_temp")) { fs.mkdirSync("./_temp"); }
    execSync(`python color.py ./raws/${img}.png ./_temp/${img}.colored.png`);
    execSync(`python expand.py ./_temp/${img}.colored.png ./_temp/${img}.template.png`);
}

function updateImage(t) {
    console.log(`Updating image for ${t}`);
    transformImage(t);
    let req_edit = http.request(`http://${host}/edit?imgname=${t}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "image/png",
            "auth": process.env.PASSWORD
        }
    });
    let readStream = fs.createReadStream(`./_temp/${t}.template.png`);
    readStream.pipe(req_edit);
    req_edit.on("response", () => {
        let req_changeThumb = http.request(`http://${host}/changeThumb?imgname=${t}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "image/png",
                "auth": process.env.PASSWORD
            }
        });
        let readStream2 = fs.createReadStream(`./_temp/${t}.colored.png`);
        readStream2.pipe(req_changeThumb);
    });
    fs.writeFileSync(`./lastUpdated/${t}.image.txt`, stamp);
}

templates.forEach(t => {
    /// COORDS
    let coordMTime = Number(fs.statSync(`./coords/${t}.txt`).mtime);
    let coordLastUpdate = Number(fs.readFileSync(`./lastUpdated/${t}.coords.txt`));
    if (coordLastUpdate < coordMTime) { updateCoords(t); }

    /// PRIORITY
    let priorityMTime = Number(fs.statSync(`./priorities/${t}.txt`).mtime);
    let priorityLastUpdate = Number(fs.readFileSync(`./lastUpdated/${t}.priority.txt`));
    if (priorityLastUpdate < priorityMTime) { updatePriority(t); }

    /// IMAGE
    let imgMTime = Number(fs.statSync(`./raws/${t}.png`).mtime);
    let imgLastUpdate = Number(fs.readFileSync(`./lastUpdated/${t}.image.txt`));
    if (imgLastUpdate < imgMTime) { updateImage(t); }
});