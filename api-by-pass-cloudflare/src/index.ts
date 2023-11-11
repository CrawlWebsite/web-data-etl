// eslint-disable-next-line @typescript-eslint/no-var-requires
require("dotenv").config()

import express from "express"
import axios from "axios"
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get("/", async (req, res) => {
  const byPassProxy =
    process.env.FLARE_SOLVERR_HOST || "http://localhost:8191/v1"

  const byPass = await axios(byPassProxy, {
    method: "POST",
    data: {
      cmd: "request.get",
      url: req.query.path,
      maxTimeout: 60000,
    },
  })

  console.log("Bypass request: ", req.query.path)
  res.send(byPass.data["solution"]["response"])
})

const port = process.env.PORT || 3000
app.listen(port, () => {
  console.log(`listening on ${port}`)
})
