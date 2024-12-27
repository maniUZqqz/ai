<?php

namespace App\Livewire\Note;

use Livewire\Component;
use App\Service\MetisClient;
use App\Models\Note;

class Index extends Component
{
    public function transcribtion()
    {

        $response = MetisClient::getClient()->audio()->transcribe([
            'model' => 'whisper-1',
            'file' => fopen('storage\audios\record_User_1.mp3', 'r'),
            // 'language' => 'en',
            'temperature' => 0.0,
            'timestamp_granularities' => ['segment', 'word'],
            'prompt' => 'This audio is in English and contains details about tasks and todos.', // توضیحات اضافی
            'response_format' => 'verbose_json',
        ]);

        $response->task; // 'transcribe'
        $response->language; // 'english'
        $response->duration; // 2.95
        $response->text; // 'Hello, how are you?'

        // foreach ($response->segments as $segment) {
        //     // $segment->index; // 0
        //     $segment->seek; // 0
        //     $segment->start; // 0.0
        //     $segment->end; // 4.0
        //     $segment->text; // 'Hello, how are you?'
        //     $segment->tokens; // [50364, 2425, 11, 577, 366, 291, 30, 50564]
        //     $segment->temperature; // 0.0
        //     $segment->avgLogprob; // -0.45045216878255206
        //     $segment->compressionRatio; // 0.7037037037037037
        //     $segment->noSpeechProb; // 0.1076972484588623
        //     $segment->transient; // false
        // }

        foreach ($response->words as $word) {
            $word->word; // 'Hello'
            $word->start; // 0.31
            $word->end; // 0.92
        }

        // dd($response->toArray()); // ['task' => 'transcribe', ...]
        $this->input = $response->text;
        $this->processNote($response->text);
        return $response->text;
    }
    public $output;

    public function processNote($input)
    {
        // تعریف پیام سیستمی برای مدل
        $systemMessage = [
            'role' => 'system',
            'content' => '
            لازم به ذکر است که ممکن است متن کمی ناخوانا بنظر بیاید. کلماتی که ناقص هستند را با حدس خود کامل کنید.
            شما باید اطلاعات زیر را از متن ورودی استخراج کنید:
            - نوع: مشخص کنید که متن مربوط به کدام دسته از یادداشت‌هاست (یاداوری، وظیفه، رویداد و ...).
            - تاپیک: موضوع اصلی یادداشت را استخراج کنید.
            - توضیحات: توضیحی کامل از یادداشت شامل زمان، مکان یا اقدامات ذکر شده.
            
            **مثال‌ها:**
            1. ورودی: "یادم باشه که به گل‌های حیاطم آب بدم ساعت 8."
            - نوع: یادآوری
            - تاپیک: آب دادن گل
            - توضیحات: آب دادن گل‌های حیاط در ساعت 8.
            2. ورودی: "باید تا فردا برای خرید مواد غذایی به فروشگاه بروم."
            - نوع: خرید
            - تاپیک: خرید مواد غذایی
            - توضیحات: خرید مواد غذایی از فروشگاه تا فردا.'
        ];

        $result = MetisClient::getClient()->chat()->create([
            'model' => 'gpt-4o-mini',
            'messages' => [
                $systemMessage,
                [
                    'role' => 'user',
                    'content' => $this->input,
                ]
            ],
            'tools' => [
                [
                    'type' => 'function',
                    'function' => [
                        'name' => 'extract_note_details',
                        'description' => 'Extract type, topic, and description from the provided note.',
                        'parameters' => [
                            'type' => 'object',
                            'properties' => [
                                'Type' => [
                                    'type' => 'string',
                                    'description' => 'The category or type of the note (e.g., reminder, task, event, etc.).if null return etc',
                                ],
                                'Topic' => [
                                    'type' => 'string',
                                    'description' => 'The main topic of the note, extracted from the text. if null return etc',
                                ],
                                'Description' => [
                                    'type' => 'string',
                                    'description' => 'A detailed description of the note, including specific details like time, place, or actions. if null return there is no description',
                                ],
                            ],
                            'required' => ['Type', 'Topic', 'Description'],
                        ],
                    ],
                ]
            ],
        ]);

        // پردازش نتیجه و دریافت آرگومان‌های ابزار
        $this->output = json_decode($result->choices[0]->message->toolCalls[0]->function->arguments, true);
        $this->submit($this->output);
        return $this->output;
    }

    public function submit($input)
    {
        $existingNote = Note::where('description', $input['Description'])->first();

        if ($existingNote) {
            return;
        }

        // Note::destroy(Note::get());
        Note::create([
            'type' => $input['Type'],
            'topic' => $input['Topic'],
            'description' => $input['Description'],
        ]);



    }

    public function render()
    {
        $notes = Note::get();
        return view('livewire.note.index', compact('notes'));
    }
}
