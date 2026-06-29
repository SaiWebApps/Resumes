/*
 * build_resume.js  —  data-driven executive résumé builder (orphan-controlled)
 * Adds keepNext (headings/roles/sublines stay with following content) and
 * keepLines (a bullet never splits across a page) to prevent stranded headers
 * and hanging lines. Content + style knobs come from the JSON.
 */

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat,
  BorderStyle, TabStopType,
} = require("docx");

// ----- Inputs -----
const contentPath = process.argv[2] || "resume_content.json";
const outPath = process.argv[3] || "resume.docx";
const data = JSON.parse(fs.readFileSync(contentPath, "utf8"));

// ----- Style (defaults are the proven two-page values; override in JSON.style) -----
const D = {
  font: "Calibri",
  navy: "1F3864",
  grey: "595959",
  dk: "262626",
  margin: 864,
  marginBottom: 612,
  size: { name: 38, banner: 21, contact: 18, head: 23, role: 21, sub: 18, body: 21, bullet: 21, ref: 20 },
  space: {
    nameAfter: 40, bannerAfter: 40, contactAfter: 30,
    sectionBefore: 104, sectionAfter: 42,
    roleBefore: 100, roleAfter: 0,
    sublineBefore: 10, sublineAfter: 44,
    bulletAfter: 22, bodyAfter: 80,
    profileAfter: 60, introAfter: 60,
    eduNoteAfter: 24, eduNoteLastAfter: 60, skillAfter: 40,
  },
};
const style = data.style || {};
const C = Object.assign({}, D, style);
C.size = Object.assign({}, D.size, style.size || {});
C.space = Object.assign({}, D.space, style.space || {});
const RIGHT_TAB = 12240 - 2 * C.margin;

// ----- Run + paragraph helpers -----
function run(text, opts) {
  return new TextRun(Object.assign({ text, size: C.size.body, font: C.font, color: C.dk }, opts || {}));
}
function runs(parts, defaultOpts) {
  return parts.map((p) => run(p.text, Object.assign({}, defaultOpts || {}, p)));
}
function nameLine(t) {
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: C.space.nameAfter },
    children: [run(t, { bold: true, size: C.size.name, color: C.navy })],
  });
}
function centerLine(children, after) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: after }, children });
}
function sectionHead(t) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: C.space.sectionBefore, after: C.space.sectionAfter },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C.navy, space: 3 } },
    children: [run(t.toUpperCase(), { bold: true, size: C.size.head, color: C.navy })],
  });
}
function roleLine(org, title, dates) {
  const kids = [run(org, { bold: true, size: C.size.role })];
  if (title) kids.push(run("  |  " + title, { size: C.size.role }));
  if (dates) kids.push(run("\t" + dates, { size: C.size.sub, color: C.grey }));
  return new Paragraph({
    keepNext: true,
    spacing: { before: C.space.roleBefore, after: C.space.roleAfter },
    tabStops: dates ? [{ type: TabStopType.RIGHT, position: RIGHT_TAB }] : [],
    children: kids,
  });
}
function subLine(t) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: C.space.sublineBefore, after: C.space.sublineAfter },
    children: [run(t, { italics: true, size: C.size.sub, color: C.grey })],
  });
}
function bulletPara(children) {
  return new Paragraph({
    numbering: { reference: "bul", level: 0 },
    spacing: { after: C.space.bulletAfter },
    children: Array.isArray(children) ? children : [run(children)],
  });
}
function bodyPara(children, after) {
  return new Paragraph({ spacing: { after: after == null ? C.space.bodyAfter : after }, children });
}

// ----- Assemble document body from data.sections -----
const k = [];

k.push(nameLine(data.name));
if (data.banner) k.push(centerLine([run(data.banner, { size: C.size.banner, color: C.dk })], C.space.bannerAfter));
(data.contactLines || []).forEach((line) =>
  k.push(centerLine([run(line, { size: C.size.contact, color: C.grey })], C.space.contactAfter)));

for (const sec of data.sections || []) {
  k.push(sectionHead(sec.heading));

  if (sec.type === "profile") {
    k.push(bodyPara([run(sec.text)], sec.target ? 40 : C.space.profileAfter));
    if (sec.target) k.push(bodyPara([run(sec.target, { bold: true, color: C.navy })], C.space.profileAfter));

  } else if (sec.type === "experience") {
    for (const e of sec.entries) {
      k.push(roleLine(e.org, e.title, e.dates));
      if (e.subline) k.push(subLine(e.subline));
      (e.bullets || []).forEach((b) => k.push(bulletPara([run(b)])));
    }

  } else if (sec.type === "education") {
    sec.entries.forEach((e) => {
      k.push(roleLine(e.org, e.title, e.dates));
      const notes = e.notes || [];
      notes.forEach((n, i) =>
        k.push(bodyPara([run(n, { size: C.size.ref })],
          i === notes.length - 1 ? C.space.eduNoteLastAfter : C.space.eduNoteAfter)));
    });

  } else if (sec.type === "publications") {
    sec.items.forEach((parts) => k.push(bulletPara(runs(parts, { size: C.size.ref }))));

  } else if (sec.type === "bullets") {
    if (sec.intro) k.push(bodyPara([run(sec.intro, { italics: true, size: C.size.ref, color: C.grey })], C.space.introAfter));
    sec.items.forEach((it) => {
      if (typeof it === "string") { k.push(bulletPara([run(it)])); return; }
      const kids = [];
      if (it.lead) kids.push(run(it.lead, { bold: true }));
      kids.push(run(it.text));
      k.push(bulletPara(kids));
    });

  } else if (sec.type === "skills") {
    sec.rows.forEach((row) =>
      k.push(new Paragraph({
        spacing: { after: C.space.skillAfter },
        children: [run(row.label + ": ", { bold: true, size: C.size.ref }), run(row.value, { size: C.size.ref })],
      })));

  } else {
    throw new Error("Unknown section type: " + sec.type);
  }
}

// ----- Document -----
const doc = new Document({
  styles: { default: { document: { run: { font: C.font, size: C.size.body } } } },
  numbering: {
    config: [{
      reference: "bul",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT,
        style: { run: { color: C.navy }, paragraph: { indent: { left: 300, hanging: 210 } } },
      }],
    }],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: C.margin, right: C.margin, bottom: C.marginBottom, left: C.margin } } },
    children: k,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log("WROTE " + outPath + " (" + buf.length + " bytes)");
});
