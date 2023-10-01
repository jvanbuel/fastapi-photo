use axum::{
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use azure_identity::DefaultAzureCredential;
use azure_storage::StorageCredentials;
use azure_storage_blobs::prelude::ClientBuilder;
use base64::{engine::general_purpose, Engine as _};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use std::sync::Arc;

const STORAGE_ACCOUNT: &str = "fastapiphoto";

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let app = Router::new()
        .route("/", get(root))
        .route("/photo", post(upload_photo));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    tracing::debug!("listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

#[derive(Deserialize, Serialize, Debug)]
struct UploadPhoto {
    name: String,
    photo_base64: String,
}

// basic handler that responds with a static string
async fn root() -> &'static str {
    "Hello, World!"
}

async fn upload_photo(Json(payload): Json<UploadPhoto>) -> impl IntoResponse {
    tracing::debug!("uploading photo: {:?}", payload);

    let photo = general_purpose::STANDARD
        .decode(payload.photo_base64)
        .unwrap();

    let token_credential = Arc::new(DefaultAzureCredential::default());
    let storage_credentials = StorageCredentials::token_credential(token_credential);
    let client =
        ClientBuilder::new(STORAGE_ACCOUNT, storage_credentials).blob_client("raw", payload.name);

    match client.put_block_blob(photo).await {
        Ok(_) => (StatusCode::OK, "photo uploaded"),
        Err(e) => {
            tracing::error!("error uploading photo: {:?}", e);
            (StatusCode::INTERNAL_SERVER_ERROR, "error uploading photo")
        }
    }
}
