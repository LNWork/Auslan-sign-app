const fs = require('fs');
const path = require('path');

const sourceFolder = __dirname;
const targetFolder = path.join(sourceFolder, 'signvideo');

if (!fs.existsSync(targetFolder)) {
  fs.mkdirSync(targetFolder);
  console.log(`Created folder: ${targetFolder}`);
}

fs.readdir(sourceFolder, (err, files) => {
  if (err) {
    return console.error('no working', err);
  }

  const mp4Files = files.filter(file => path.extname(file) === '.mp4');

 
  mp4Files.forEach(file => {
    const oldPath = path.join(sourceFolder, file);
    const newPath = path.join(targetFolder, file);

    fs.rename(oldPath, newPath, (err) => {
      if (err) {
        return console.error(`Error moving file ${file}:`, err);
      }
      console.log(`Moved: ${file} to ${newPath}`);
    });
  });

  if (mp4Files.length === 0) {
    console.log('No .mp4 files found in the current directory.');
  }
});
