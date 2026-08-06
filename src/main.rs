#[macro_use] extern crate rocket;

use std::sync::Arc;
use rocket::serde::json::Json;
use rocket::serde::{Deserialize, Serialize};
use rocket_firebase_auth::{FirebaseAuth, FirebaseToken};

struct ServerState {
    auth: FirebaseAuth,
}

#[derive(Serialize,Deserialize)]
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
        generate
    ]).manage(ServerState { auth: firebase_auth })
}

#[get("/")]
fn status() -> &'static str {
    "running"
}

#[post("/ai/generate")]
fn generate(token: FirebaseToken) -> Result<Json<AIResponse>, String> {
    Ok(Json(AIResponse {
        output: "success".to_string(),
    }))
}