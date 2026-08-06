#[macro_use] extern crate rocket;

use std::sync::Arc;
use firebase_auth::{FirebaseAuth, FirebaseAuthState, FirebaseUser};



#[launch]
async fn rocket() -> _ {

    let project_id = "your-firebase-project-id";
    let firebase_auth = FirebaseAuth::new(project_id).await;

    // 2. Wrap it in an Arc to share safely across threads
    let auth_state = FirebaseAuthState {
        firebase_auth: Arc::new(firebase_auth),
    };

    rocket::build().mount("/", routes![
        status
    ])
}

#[get("/")]
fn status() -> &'static str {
    "running"
}