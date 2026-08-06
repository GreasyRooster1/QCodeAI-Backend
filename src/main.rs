#[macro_use] extern crate rocket;

use std::sync::Arc;
use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Request, Response};
use rocket::http::Header;
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
    .mount("/",routes![status,all_options])
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

pub struct CORS;

#[rocket::async_trait]
impl Fairing for CORS {
    fn info(&self) -> Info {
        Info {
            name: "Add CORS headers to responses",
            kind: Kind::Response
        }
    }

    async fn on_response<'r>(&self, _request: &'r Request<'_>, response: &mut Response<'r>) {
        response.set_header(Header::new("Access-Control-Allow-Origin", "http://localhost:3000, ai.esporterz.com"));
        response.set_header(Header::new("Access-Control-Allow-Methods", "POST, GET, PATCH, DELETE, OPTIONS"));
        response.set_header(Header::new("Access-Control-Allow-Headers", "*"));
        response.set_header(Header::new("Access-Control-Allow-Credentials", "true"));
    }
}

#[options("/<_..>")]
fn all_options() {
    /* Intentionally left empty */
}