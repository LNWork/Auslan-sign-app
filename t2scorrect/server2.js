const express = require('express');
const path = require('path');
const app = express();

app.use('/signvideo', express.static(path.join(__dirname, 'signvideo')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index2.html'));
});

const port = 3001;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
