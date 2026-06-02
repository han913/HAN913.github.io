const { getStore } = require("@netlify/blobs");

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  try {
    const body = JSON.parse(event.body || "{}");

    if (!body.secure_url || !body.public_id) {
      return { statusCode: 400, body: "Missing image data" };
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

    return {
      statusCode: 200,
      body: JSON.stringify({ ok: true })
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: err.message
    };
  }
};