import { Entity, PrimaryGeneratedColumn, Column, Unique } from "typeorm"
import { AppDataSource } from "../database/db"

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number

  @Column()
  name: string

  @Column({ unique: true })
  phone: string
}

export const UserRepository = () => {
  return AppDataSource.getRepository(User)
}
