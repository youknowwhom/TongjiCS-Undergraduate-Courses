import 'virtual:uno.css'
import '@unocss/reset/tailwind.css'

import $ from 'jquery'

import testCode from "./test.c?raw"

import * as monaco from 'monaco-editor'
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
self.MonacoEnvironment = { getWorker: () => new editorWorker() }

class CPF {
  constructor() {
    this.editor = monaco.editor.create(
      document.getElementById('cm-container'),
      {
        value: testCode,
        language: 'plain',
        minimap: {
          enabled: false
        },
        cursorBlinking: "smooth",
        automaticLayout: true,
        fixedOverflowWidgets: true,
      },
    )
    this.editor.getModel().onDidChangeContent(() => {
      window.cpf.flush()
    })
    window.addEventListener("resize", () => {
      this.editor.layout()
    })
  }

  callCompiler(code_str) {
    if (!this.compiler) return
    this.compiler.process(code_str)
      .then(JSON.parse)
      .then((result) => {
        if (window.treeView) {
          window.treeView.draw(result.ast)
        }
        this.codeHighlight(result.lexer, code_str)
        for (const tid of ["goto", "action", "process"]) {
          $(`#${tid}-table`).html(this.tableHTML(result[tid]))
        }
      })
  }

  /**
   * @param {Array} token_list 
   * @param {string} code 
   */
  codeHighlight(token_list, code) {
    const lines = code.split("\n")
    const getHightlightClass = (token) => {
      const c = []
      const ci = []
      if (token.prop === "unknown") {
        c.push(`cpf-unique-token-invalid`)
        c.push("cpf-invalid-token")
        ci.push("cpf-invalid-token")
      } else {
        if (!!this.drawAllToken) {
          c.push(`cpf-unique-token-${token.id}`)
          c.push("cpf-all-token")
        }
        if (/.*constant/.test(token.prop)) {
          ci.push(`cpf-token-constant`)
        } else if (/kw_.*/.test(token.prop)) {
          ci.push(`cpf-token-keyword`)
        } else if (/identifier.*/.test(token.prop)) {
          ci.push(`cpf-token-identifier`)
        } else {
          ci.push(`cpf-token-${token.prop}`)
        }
      }
      console.error(`${JSON.stringify(token.loc)} "${token.content}" ==> ${c.join(" ") + ci.join(" ")}`)
      return {
        "inline": ci.join(" "),
        "normal": c.join(" ")
      }
    }
    this.editor.getModel().deltaDecorations(this.editor.getModel().getAllDecorations().map(d => d.id), [])
    this.editor.getModel().deltaDecorations(
      [],
      token_list
        .map((token) => {
          // ensure token exists in code
          if (token.prop === "unknown") {
            console.error("unknown: ", JSON.stringify(token))
            token.content = "_"
          }
          const actualRow = lines[token.loc.row - 1]
          if (
            !!actualRow && (actualRow.substring(
              token.loc.col - 1,
              token.loc.col - 1 + token.content.length
            ) === token.content) || token.prop === "unknown"
          ) {
            return token
          }
          console.error(`ignored token : ${JSON.stringify(token)}`)
        })
        .filter(t => !!t)
        .map(token => {
          const classes = getHightlightClass(token)
          return {
            range: new monaco.Range(
              token.loc.row,
              token.loc.col,
              token.loc.row,
              token.loc.col + token.content.length
            ),
            options: {
              isWholeLine: false,
              className: classes["normal"],
              inlineClassName: classes["inline"],
            }
          }
        })
    )
  }

  flush() {
    this.callCompiler(this.editor.getModel().getValue())
  }

  setCompiler(compiler) {
    this.compiler = compiler
  }

  switchRightTab(right_id) {
    const tab_bg = "cpf-active-tab"
    const it_to_display = document.getElementById(`${right_id}-container`)
    if (!!it_to_display) {
      const right_items = document.getElementsByClassName("cpf-right")
      for (const it of right_items) {
        it.style.display = "none"
      }
      it_to_display.style.display = "inline"
    }
    const tab_to_display = document.getElementById(`${right_id}-tab-button`)
    if (!!tab_to_display) {
      const tabs = document.getElementsByClassName("cpf-tab-button")
      for (const tab of tabs) {
        tab.classList.remove(tab_bg)
      }
      tab_to_display.classList.add(tab_bg)
    }
    {
      const zooms = document.getElementsByClassName("ast-zoom-button")
      for (const zoomBtn of zooms) {
        zoomBtn.style.display = (right_id === "ast" ? "inline" : "none")
      }
    }
  }

  tableHTML(arr) {
    const HTML = []
    HTML.push("<table>")
    for (const [i, row] of arr.entries()) {
      HTML.push("<tr>")
      for (const [j, col] of row.entries()) {
        let style = ""
        if (j === 0 && i !== 0) {
          style = "position: sticky; left: 0; z-index: 2;"
        } else if (i === 0 && j !== 0) {
          style = "position: sticky; top: 0; z-index: 1;"
        } else if (i === 0 && j === 0) {
          style = "position: sticky; top: 0; left: 0; z-index: 3;"
        }
        HTML.push(`<td style="${style}">`)
        HTML.push(col)
        HTML.push(`</td>`)
      }
      HTML.push("</tr>")
    }
    HTML.push("</table>")
    return HTML.join("")
  }
}

window.cpf = new CPF()
window.cpf.switchRightTab('ast')
window.cpf.flush()
const channel = new QWebChannel(window.qt.webChannelTransport, function (channel) {
  window.cpf.setCompiler(channel.objects.compiler)
  window.cpf.flush()
});
