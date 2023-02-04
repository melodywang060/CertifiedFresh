const express = require('express')
const app = express()
const cookieSession = require('cookie-session')
const ejs = require('ejs')
const multer = require("multer")
const path = require('path')
const fs = require('fs')
const crypto = require('crypto')
const {spawn} = require('child_process')

const PORT = 4000

app.set('view engine', 'ejs')
app.use(express.static(`${__dirname}/static`))

app.use(cookieSession({
  name: 'chocolatechip',
  keys: ['asfdasdfsdhfjsdfkjsdkhfsd', 'dkjksdfhsdfsdhsdsdaksdfakhfsdasdfkhsdfahjsdakhsdfajkshjsd']
}))

const upload = multer({
  dest: "static/images/plants"
})


app.get('/', (req, res) => {
  res.render('index')
})

function getPlants (req, res, next) {
  if (req.session.plants === undefined) {
    res.locals.plants = []
    next()
  }
  else {
    res.locals.plants = req.session.plants
    next()
  }
}

function formatDate(date) {
  return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`
}

function saveImage(req, res, next) {
  const tempPath = req.file.path;
  const imageName = crypto.randomBytes(8).toString('hex')
  const targetPath = path.join(__dirname, `./static/images/plants/${imageName}.png`)
  res.locals.imageName = imageName

  if (path.extname(req.file.originalname).toLowerCase() === ".png" || path.extname(req.file.originalname).toLowerCase() === ".jpg" || path.extname(req.file.originalname).toLowerCase() === ".jpeg") {
    fs.rename(tempPath, targetPath, err => {
      if (err) {
        console.log(err)
        res.send(err)
      }

      next()
    })
  } else {
    fs.unlink(tempPath, err => {
      if (err) {
        console.log(err)
        res.send(err)
      }

      res.send("Only .png/.jpg/.jpeg files are allowed!");
    });
  }
}

function runScript (req, res, next) {
  const python = spawn('python', ['script.py', `-i images/plants/${res.locals.imageName}.png`]);
  // collect data from script
  // console.log("???")
  // python.stdout.on('data', function (data) {
  //   console.log('Pipe data from python script ...');
  //   console.log(data.toString())
  //   next()
  // });
  next()
}

app.post('/addplant', [upload.single("file"), saveImage, runScript], (req, res) => {
  const plantData = {
    name: req.body.name,
    water: req.body.water,
    lastWatered: new Date(),
    lastWateredString: formatDate(new Date()),
    type: req.body.type,
    image: [`images/plants/${res.locals.imageName}.png`],
    health: [10],
    dates: [formatDate(new Date())],
  }

  if (req.session.plants === undefined) {
    req.session.plants = []
  }

  req.session.plants.push(plantData)
  res.redirect('/myplants')
})

app.get('/myplants', [getPlants], (req, res) => {
  for (let i = 0; i < res.locals.plants.length; i++) {
    const tempDate = new Date(res.locals.plants[i].lastWatered)
    tempDate.setDate(tempDate.getDate() + parseInt(res.locals.plants[i].water))
    res.locals.plants[i].nextWaterString = formatDate(tempDate)
  }
  res.render('myplants', {plants: res.locals.plants})
})

app.get('/newseeds', (req, res) => {
  res.render('newseeds')
})

app.get('/mygrowth', [getPlants], (req, res) => {
  res.render('mygrowth', {plants: res.locals.plants})
})

app.listen(process.env.PORT || PORT, () => console.log("Server is running..."));
