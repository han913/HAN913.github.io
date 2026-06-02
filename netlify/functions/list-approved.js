const { connectLambda, getStore } = require("@netlify/blobs");

function json(statusCode, data) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store"
    },
    body: JSON.stringify(data)
  };
}

exports.handler = async (event) => {
  try {
    connectLambda(event);

    const store = getStore("graduation-album");
    const approved = await store.get("approved", { type: "json" }) || [];

    return json(200, approved);
  } catch (err) {
    console.error("list-approved error:", err);

    return json(500, {
      ok: false,
      error: err.message
    });
  }
};