-- Pandoc-фільтр для звітів: Markdown (як на GitHub) -> .docx
--  * HTML <sub>/<sup>/<br> перетворюються на рідне форматування Word
--  * відносні посилання на файли репозиторію стають посиланнями на GitHub
--  * перший заголовок H1 стає назвою документа

local function is_br(el)
  local t = el.text:lower()
  return el.format == "html" and (t == "<br>" or t == "<br/>" or t == "<br />")
end

-- Збираємо вміст між <sub>…</sub> у Subscript (аналогічно <sup>)
local function wrap_scripts(inlines)
  local out, buf, kind = pandoc.List(), nil, nil
  for _, el in ipairs(inlines) do
    local tag = el.t == "RawInline" and el.format == "html" and el.text:lower() or ""
    local open, close = tag:match("^<(su[bp])>$"), tag:match("^</(su[bp])>$")
    if open and not buf then
      buf, kind = pandoc.List(), open
    elseif close and buf and close == kind then
      out:insert(kind == "sub" and pandoc.Subscript(buf) or pandoc.Superscript(buf))
      buf, kind = nil, nil
    elseif el.t == "RawInline" and is_br(el) then
      (buf or out):insert(pandoc.LineBreak())
    else
      (buf or out):insert(el)
    end
  end
  if buf then out:extend(buf) end
  return out
end

-- Абзаци, які Word зберіг як <p>…</p>, розбираємо як звичайний Markdown
local function unwrap_p(el)
  if el.format ~= "html" then return nil end
  local inner = el.text:match("^%s*<p>(.-)</p>%s*$")
  if inner then return pandoc.read(inner, "gfm+raw_html").blocks end
end

function Pandoc(doc)
  local repo_blob = doc.meta.repo_blob and pandoc.utils.stringify(doc.meta.repo_blob)

  doc = doc:walk({ RawBlock = unwrap_p })
  doc = doc:walk({
    Inlines = wrap_scripts,
    Link = function(el)
      local t = el.target
      if not repo_blob or t:match("^%a[%w+.-]*:") or t:match("^[#/]") then return nil end
      el.target = repo_blob .. "/" .. t
      return el
    end,
  })

  for i, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then
      if not doc.meta.title then doc.meta.title = b.content end
      doc.blocks:remove(i)
      break
    end
  end
  return doc
end
