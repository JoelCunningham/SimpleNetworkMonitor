import { EditField } from '#components/fields';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('EditField', () => {
  let component: EditField;
  let fixture: ComponentFixture<EditField>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditField],
    }).compileComponents();

    fixture = TestBed.createComponent(EditField);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
