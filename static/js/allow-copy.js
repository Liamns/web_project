(function agent() {
    let unlock = false
    document.addEventListener('allow_copy', (event) => {
      unlock = event.detail.unlock
    })

    const copyEvents = [
      'copy',
      'cut',
      'contextmenu',
      'selectstart',
      'mousedown',
      'mouseup',
      'mousemove',
      'keydown',
      'keypress',
      'keyup'
    ]
    const rejectOtherHandlers = (e) => {
      if (unlock) {
        e.stopPropagation()
        if (e.stopImmediatePropagation) 
          e.stopImmediatePropagation()
      }
    }
    copyEvents.forEach((evt) => {
      document
        .documentElement
        .addEventListener(evt, rejectOtherHandlers, {capture: true})
    })
  })()