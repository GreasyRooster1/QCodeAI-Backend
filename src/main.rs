#[macro_use] extern crate rocket;

use std::sync::Arc;
use rocket_firebase_auth::{FirebaseAuth, FirebaseToken};

struct ServerState {
    auth: FirebaseAuth,
}

struct AIResponse{
    output:String,
}

#[launch]
async fn rocket() -> _ {

    let firebase_auth = FirebaseAuth::builder()
        .json_file("service-account.json")
        .build()
        .unwrap();

    rocket::build()
    .mount("/",routes![status])
    .mount("/api", routes![
        status
    ]).manage(ServerState { auth: firebase_auth })
}

#[get("/")]
fn status() -> &'static str {
    "running"
}

#[post("/ai/generate")]
fn generate(token: FirebaseToken) -> &'static str {
    "running"
}