import { useRef } from "react";

function FileUpload({
  files,
  setFiles,
}) {

  const inputRef = useRef(null);

  const handleFiles = (selectedFiles) => {

    const validFiles = Array.from(selectedFiles).filter(
      (file) => {

        const extension =
          "." +
          file.name
            .split(".")
            .pop()
            .toLowerCase();

        return [
          ".pdf",
          ".docx",
          ".csv",
          ".txt",
        ].includes(extension);
      }
    );

    setFiles((previous) => [
      ...previous,
      ...validFiles,
    ]);
  };


  const handleInputChange = (event) => {
    handleFiles(event.target.files);
  };


  const removeFile = (index) => {

    setFiles((previous) =>
      previous.filter(
        (_, fileIndex) =>
          fileIndex !== index
      )
    );
  };


  return (
    <div>

      <label className="mb-2 block text-sm font-medium text-gray-300">
        Project Documents
      </label>

      <div
        onClick={() => inputRef.current?.click()}
        className="cursor-pointer rounded-2xl border-2 border-dashed border-gray-700 bg-[#0b0f17] px-6 py-10 text-center transition hover:border-indigo-500 hover:bg-[#0e1420]"
      >

        <div className="mb-4 text-4xl">
          📁
        </div>

        <p className="font-medium text-gray-300">
          Upload project documents
        </p>

        <p className="mt-2 text-sm text-gray-500">
          Click to browse PDF, DOCX, CSV or TXT files
        </p>

        <p className="mt-1 text-xs text-gray-600">
          Multiple files supported
        </p>

        <input
          ref={inputRef}
          type="file"
          multiple
          accept=".pdf,.docx,.csv,.txt"
          onChange={handleInputChange}
          className="hidden"
        />

      </div>


      {/* Files */}
      {files.length > 0 && (

        <div className="mt-4 space-y-2">

          {files.map((file, index) => (

            <div
              key={`${file.name}-${index}`}
              className="flex items-center justify-between rounded-xl border border-gray-800 bg-[#111722] px-4 py-3"
            >

              <div className="flex min-w-0 items-center gap-3">

                <span className="text-lg">
                  📄
                </span>

                <div className="min-w-0">

                  <p className="truncate text-sm text-gray-300">
                    {file.name}
                  </p>

                  <p className="text-xs text-gray-600">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>

                </div>

              </div>


              <button
                type="button"
                onClick={() => removeFile(index)}
                className="ml-4 text-gray-600 transition hover:text-red-400"
              >
                ✕
              </button>

            </div>

          ))}

        </div>

      )}

    </div>
  );
}

export default FileUpload;