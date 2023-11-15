// eslint-disable-next-line @typescript-eslint/no-var-requires
require("dotenv").config()

import { DataSource } from "typeorm"

export const AppDataSource = new DataSource({
  type: "postgres",
  host: process.env.POSTGRES_HOST || "localhost",
  port: 5432,
  username: "admin",
  password: "admin",
  database: "postgres",
  synchronize: true,
  logging: false,
  entities: ["build/src/entities/**/*.entity.js"],
})
