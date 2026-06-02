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

function getHeader(event, name) {
  const target = name.toLowerCase();
  const headers = event.headers || {};

  for (const key of Object.keys(headers)) {
    if (key.toLowerCase() === target) {
      return headers[key];
    }
  }

  return "";
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return json(405, {
      ok: false,
      error: "Method Not Allowed"
    });
  }

  try {
    connectLambda(event);

    const pass = getHeader(event, "x-admin-pass");

    if (!process.env.ADMIN_PASS || pass !== process.env.ADMIN_PASS) {
      return json(401, {
        ok: false,
        error: "Unauthorized"
      });
    }

    const body = JSON.parse(event.body || "{}");
    const id = body.id;

    if (!id) {
      return json(400, {
        ok: false,
        error: "Missing photo id"
      });
    }

    const store = getStore("graduation-album");
    let approved = await store.get("approved", { type: "json" }) || [];

    const exists = approved.some(function (photo) {
      return String(photo.id) === String(id);
    });

    if (!exists) {
      return json(404, {
        ok: false,
        error: "Photo not found"
      });
    }

    approved = approved.filter(function (photo) {
      return String(photo.id) !== String(id);
    });

    await store.set("approved", JSON.stringify(approved), {
      contentType: "application/json"
    });

    return json(200, {
      ok: true,
      success: true,
      message: "已从网站移除"
    });
  } catch (err) {
    console.error("delete-approved error:", err);

    return json(500, {
      ok: false,
      error: err.message
    });
  }
};