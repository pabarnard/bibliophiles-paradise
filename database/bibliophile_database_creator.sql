-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bibliophile_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bibliophile_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bibliophile_schema` DEFAULT CHARACTER SET utf8 ;
USE `bibliophile_schema` ;

-- -----------------------------------------------------
-- Table `bibliophile_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bibliophile_schema`.`users` (
  `id` VARCHAR(255) NOT NULL,
  `username` VARCHAR(3072) NULL,
  `email` VARCHAR(3072) NULL,
  `password` VARCHAR(3072) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bibliophile_schema`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bibliophile_schema`.`books` (
  `id` VARCHAR(255) NOT NULL,
  `google_volume_id` VARCHAR(3072) NULL,
  `title` VARCHAR(3072) NULL,
  `authors` VARCHAR(3072) NULL,
  `publication_date` DATE NULL,
  `page_count` INT NULL,
  `thumbnail` VARCHAR(3072) NULL,
  `isbn13` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bibliophile_schema`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bibliophile_schema`.`reviews` (
  `user_id` VARCHAR(255) NOT NULL,
  `book_id` VARCHAR(255) NOT NULL,
  `text` TEXT NULL,
  `rating` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `book_id`),
  INDEX `fk_users_has_books_books2_idx` (`book_id` ASC) VISIBLE,
  INDEX `fk_users_has_books_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_books_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `bibliophile_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_books_books2`
    FOREIGN KEY (`book_id`)
    REFERENCES `bibliophile_schema`.`books` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bibliophile_schema`.`bookshelves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bibliophile_schema`.`bookshelves` (
  `user_id` VARCHAR(255) NOT NULL,
  `book_id` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`user_id`, `book_id`),
  INDEX `fk_users_has_books_books3_idx` (`book_id` ASC) VISIBLE,
  INDEX `fk_users_has_books_users2_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_books_users2`
    FOREIGN KEY (`user_id`)
    REFERENCES `bibliophile_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_books_books3`
    FOREIGN KEY (`book_id`)
    REFERENCES `bibliophile_schema`.`books` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bibliophile_schema`.`thoughts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bibliophile_schema`.`thoughts` (
  `bookshelves_user_id` VARCHAR(255) NOT NULL,
  `bookshelves_book_id` VARCHAR(255) NOT NULL,
  `text` TEXT NULL,
  `is_public` TINYINT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `fk_thoughts_bookshelves1_idx` (`bookshelves_user_id` ASC, `bookshelves_book_id` ASC) VISIBLE,
  CONSTRAINT `fk_thoughts_bookshelves1`
    FOREIGN KEY (`bookshelves_user_id` , `bookshelves_book_id`)
    REFERENCES `bibliophile_schema`.`bookshelves` (`user_id` , `book_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
