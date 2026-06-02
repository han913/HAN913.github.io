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
  if (event.httpMethod !== "POST") {
    return json(405, {
      ok: false,
      success: false,
      error: "Method Not Allowed"
    });
  }

  try {
    connectLambda(event);

    const body = JSON.parse(event.body || "{}");

    if (!body.secure_url || !body.public_id) {
      return json(400, {
        ok: false,
        success: false,
        error: "Missing image data"
      });
    }

    const store = getStore("graduation-album");
    const pending = await store.get("pending", { type: "json" }) || [];

    const photo = {
      id: Date.now().toString() + "-" + Math.random().toString(36).slice(2),
      name: body.name || "匿名",
      message: body.message || "",
      public_id: body.public_id,
      secure_url: body.secure_url,
      width: body.width || 0,
      height: body.height || 0,
      format: body.format || "",
      created_at: new Date().toISOString()
    };

    pending.unshift(photo);

    await store.set("pending", JSON.stringify(pending), {
      contentType: "application/json"
    });

    return json(200, {
      ok: true,
      success: true,
      message: "上传成功，等待审核"
    });
  } catch (err) {
    console.error("submit-photo error:", err);

    return json(500, {
      ok: false,
      success: false,
      error: err.message
    });
  }
};