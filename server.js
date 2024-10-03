const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const videoFolder = path.join(__dirname, 'signvideo');

app.use(express.static(path.join(__dirname)));

app.get('/video/:word', (req, res) => {
  const word = req.params.word;
  const videoPath = path.join(videoFolder, `${word}.mp4`);

  if (fs.existsSync(videoPath)) {
    res.sendFile(videoPath);
  } else {
    res.status(404).send('Video not found');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
