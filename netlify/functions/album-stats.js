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

    const pending = await store.get("pending", { type: "json" }) || [];
    const approved = await store.get("approved", { type: "json" }) || [];

    const messages = approved
      .filter((photo) => photo.message && String(photo.message).trim())
      .slice(0, 30)
      .map((photo) => ({
        name: photo.name || "匿名",
        message: String(photo.message).trim(),
        created_at: photo.created_at || "",
        approved_at: photo.approved_at || ""
      }));

    return json(200, {
      ok: true,
      pendingCount: pending.length,
      approvedCount: approved.length,
      messages
    });
  } catch (err) {
    console.error("album-stats error:", err);

    return json(500, {
      ok: false,
      error: err.message
    });
  }
};