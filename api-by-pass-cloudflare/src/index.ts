// eslint-disable-next-line @typescript-eslint/no-var-requires
require("dotenv").config()
import FormData from "form-data"
import express from "express"
import axios from "axios"
import bodyParser from "body-parser"

import { AppDataSource } from "./database/db"
import { UserRepository } from "./entities"

const app = express()
app.use(bodyParser.json())

// respond with "hello world" when a GET request is made to the homepage
app.get("/", async (req, res) => {
  try {
    const { cmd, path, postData } = req.query
    const byPassProxy =
      process.env.FLARE_SOLVERR_HOST || "http://localhost:8191/v1"

    const byPass = await axios(byPassProxy, {
      method: "POST",
      data: {
        cmd: `request.${cmd}`,
        url: path,
        postData,
        maxTimeout: 60000,
      },
    })

    console.log("Bypass request: ", req.query.path)
    res.send(byPass.data["solution"]["response"])
  } catch (err) {
    console.log(err)
    res.sendStatus(404)
  }
})

app.post("/user/bulk", async (req, res) => {
  try {
    const users = req.body.users

    const uniqueList = Object.values(
      users.reduce((acc: any, user: any) => {
        acc[user.phone] = user
        return acc
      }, {})
    )
    console.log("Users: ", uniqueList)

    await UserRepository().upsert(
      uniqueList.map((user: any) => {
        return {
          name: user.name,
          phone: user.phone,
        }
      }),
      {
        conflictPaths: ["phone"],
        skipUpdateIfNoValuesChanged: true, // Only supports postgresql
      }
    )

    res.send("ok")
  } catch (err) {
    console.log(err)
    res.sendStatus(404)
  }
})

const port = process.env.PORT || 3000
app.listen(port, async () => {
  await AppDataSource.initialize()

  console.log(`listening on ${port}`)
})
