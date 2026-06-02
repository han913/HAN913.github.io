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
    const barrages = await store.get("barrages", { type: "json" }) || [];

    const approvedMessages = approved
      .filter((photo) => photo.message && String(photo.message).trim())
      .map((photo) => ({
        id: photo.id,
        name: photo.name || "匿名",
        message: String(photo.message).trim(),
        created_at: photo.created_at || "",
        approved_at: photo.approved_at || "",
        source: "photo"
      }));

    const directBarrages = barrages
      .filter((item) => item.message && String(item.message).trim())
      .map((item) => ({
        id: item.id,
        name: item.name || "匿名",
        message: String(item.message).trim(),
        created_at: item.created_at || "",
        source: "barrage"
      }));

    const messages = [...directBarrages, ...approvedMessages]
      .sort((a, b) => {
        const ta = new Date(a.created_at || a.approved_at || 0).getTime();
        const tb = new Date(b.created_at || b.approved_at || 0).getTime();
        return tb - ta;
      })
      .slice(0, 80);

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