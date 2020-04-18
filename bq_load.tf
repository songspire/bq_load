variable "project_id" {
  type = string
  default = "tmp1-271812"
}

variable "bucket_name" {
  type = string
  default = "new-books"
}

variable "bucket_delete_age" {
  type = number
  default = 1
}

variable "dataset" {
  type = string
  default = "new_books"
}

variable "bq_users" {
  type = list(string)
  default = []
  description = "A list of the emails of users that will be granted OWNER permissions on the BQ dataset"
}

provider "google" {
  project = var.project_id
  region  = "europe-west3"
  zone    = "europe-west3-a"
}

resource "google_storage_bucket" "new-books" {
  name = var.bucket_name
  location = "EU"

  force_destroy = true

  lifecycle_rule {
    condition {
      age = var.bucket_delete_age
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_project_iam_custom_role" "new-books-cloud-function" {
  role_id = "NewBooksCloudFunction"
  title = "New Books Cloud Function"
  permissions = [
    "storage.buckets.get", 
    "storage.buckets.list", 
    "storage.objects.get", 
    "storage.objects.list",
    "bigquery.jobs.create",
    "bigquery.tables.create"
  ]
}

resource "google_service_account" "new-books-cloud-function" {
  account_id   = "new-books-cloud-function"
  display_name = "New Books Cloud Function"
}

resource "google_project_iam_member" "project" {
  project = var.project_id
  role    = "projects/tmp1-271812/roles/NewBooksCloudFunction"
  member  = "serviceAccount:${google_service_account.new-books-cloud-function.email}"
}

resource "google_cloudfunctions_function" "new-books" {
  name        = "new-books"
  description = "New books data loading"
  runtime     = "python37"

  available_memory_mb   = 128
  # trigger_bucket        = google_storage_bucket.new-books.name
  timeout               = 60
  max_instances         = 4
  entry_point           = "books_load"
  service_account_email = google_service_account.new-books-cloud-function.email
  source_repository {
    url = "https://source.developers.google.com/projects/tmp1-271812/repos/books_load/moveable-aliases/master/paths/"
  }
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource = google_storage_bucket.new-books.name
  }
  labels = {
    env = "prod"
    app = "new-books"
  }
}

resource "google_bigquery_dataset" "new-books" {
  dataset_id                  = var.dataset
  friendly_name               = "New Books"
  description                 = "This is the dataset to load new books"
  location                    = "EU"
  default_table_expiration_ms = 3600000

  labels = {
    env = "prod"
    app = "new-books"
  }

  access {
    role          = "OWNER"
    user_by_email = google_service_account.new-books-cloud-function.email
  }

  dynamic "access" {
    for_each = var.bq_users
    content {
      role = "OWNER"
      user_by_email = access.value
    }
  }
  
}


output "bucket" {
  value = google_storage_bucket.new-books.name
}

output "BQ_dataset" {
  value = google_bigquery_dataset.new-books.id
}

