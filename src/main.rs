#[macro_use] extern crate rocket;

use std::sync::Arc;
use rocket_firebase_auth::{FirebaseAuth, FirebaseToken};

struct ServerState {
    auth: FirebaseAuth,
}

#[launch]
async fn rocket() -> _ {

    let firebase_auth = FirebaseAuth::builder()
        .json_file("service-account.json")
        .build()
        .unwrap();

    rocket::build().mount("/", routes![
        status
    ])
}

#[get("/")]
fn status() -> &'static str {
    "running"
}

#[post("/api/ai/generate")]
fn generate() -> &'static str {
    "running"
}